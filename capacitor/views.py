# -*- coding: utf-8 -*-
from flask import jsonify, request, g
from flask.views import MethodView
import redis
import json

from capacitor import app
from capacitor import response
from capacitor import security


class ActorView(MethodView):

    pool = redis.ConnectionPool(host=app.config["REDIS_HOST"],
                                port=6379, db=0)

    @property
    def _secret_key(self):
        secret = self.get_setting("secret_key")
        if not secret:
            raise Exception("'secret_key' needed")
        return self.get_setting("secret_key")

    @property
    def _current_access_token(self):
        access_token = None
        if "access_token" in request.cookies:
            access_token = request.cookies["access_token"]
        elif "Access-Token" in request.headers:
            access_token = request.headers["Access-Token"]
        else:
            pass
        return access_token

    def get_current_user(self):
        curr_access_token = self._current_access_token
        if not curr_access_token:
            return None
        # expiration: 365 days
        args = (self._secret_key, "access_token",
                curr_access_token, 365)
        return security.decode_signed_value(*args)

    @property
    def current_user(self):
        if not hasattr(g, 'current_user'):
            g.current_user = self.get_current_user()
        return g.current_user

    def get_setting(self, name, default=None):
        rv = default
        if name.upper() in app.config:
            rv = app.config[name.upper()]
        return rv

    @property
    def cache(self):
        """
        cache = {
            "mirrors": {},
            "notices": {},
            "users": {}
        }
        """
        if hasattr(g, "cache"):
            return g.cache
        g.cache = redis.StrictRedis(connection_pool=self.pool)
        return g.cache

    def get_cache(self, k, default=None):
        rv = json.loads(self.cache.get(k))
        return rv if rv else default

    def set_cache(self, k, v):
        value = json.dumps(v)
        return self.cache.set(k, value)


class Mirrors(ActorView):

    def _build_mirror(self, data):
        # set some flags
        url = "{}://{}{}".format(data["protocol"], data["host"], data["path"])
        has_help = True if data["help_url"] else False
        is_muted = True if data["muted_at"] else False
        return dict(
            cname=data["cname"],
            url=url,
            full_name=data["full_name"],
            help_url=data["help_url"],
            has_help=has_help,
            created_at=data["created_at"],
            upstream_url=data["upstream_url"],
            muted_at=data["muted_at"],
            is_muted=is_muted,
            sync_status=None,
            synced_at=None,
            comment=None,
            has_comment=False,
            size=None,)

    def _check_cname(self, cname):
        errors = []
        if cname:
            # TODO: cname consists of '[a-z]' and '-'.
            pass

        return errors

    def get(self, cname):
        # return list of mirrors
        errors = self._check_cname(cname)
        if errors:
            return response.unprocessable_entity(errors=errors)

        mirrors_cached = self.get_cache("mirrors")
        if mirrors_cached is None:
            return response.not_found("No cache for mirrors.")

        if cname is None:
            rv = dict(count=0, targets=[])
            rv["targets"] = mirrors_cached.values()
            rv["count"] = len(rv["targets"])
            return jsonify(rv)
        else:
            if cname not in mirrors_cached.keys():
                return response.not_found("No such resource.")

            return jsonify(mirrors_cached[cname])

    def _check_post_params(self, raw_json_data):
        errors = []
        if raw_json_data:
            pass
            '''
            fields = ["cname", "full_name", "protocol", "host", "path",
                      "help", "created_at", "upstream_url", ]
            fields_missing = [key for key in fields
                              if key not in raw_json_data.keys()]
            if fields_missing:
                error = dict(
                    resource="mirrors/{}".format(raw_json_data["cname"]),
                    fields=fields_missing,
                    code="missing_field",)
                errors.append(error)
            '''

        return errors

    @security.authenticated
    def post(self):
        json_data = request.get_json(silent=True)
        if not json_data:
            return response.bad_request("Problems parsing JSON.")
        errors = self._check_post_params(json_data)
        if errors:
            return response.unprocessable_entity(errors=errors)

        mirrors_cached = self.get_cache("mirrors")
        if not mirrors_cached:
            mirrors_cached = {}

        mirrors_created = mirrors_cached.copy()
        for mirror_meta in json_data["targets"]:
            cname = mirror_meta["cname"]
            # Just pass existed items and don't update it here!
            if cname in mirrors_cached.keys():
                continue
            mirrors_created[cname] = self._build_mirror(mirror_meta)
        if mirrors_created:
            self.set_cache("mirrors", mirrors_created)
            return response.created()
        else:
            return response.ok("Nothing changed.")

    @security.authenticated
    def put(self, cname):
        json_data = request.get_json(silent=True)
        if json_data is None:
            return response.bad_request("Problems parsing JSON.")

        mirrors_cached = self.get_cache("mirrors")
        if mirrors_cached is None:
            return response.bad_request("No cache for mirrors.")

        return response.not_implemented("API hasn't implemented.")

    @security.authenticated
    def delete(self, cname):
        return response.not_implemented("API hasn't implemented.")


class Notices(ActorView):

    def _build_notice(self, data):
        is_muted = True if data["muted_at"] else False
        return dict(
            id=data["id"],
            created_at=data["created_at"],
            muted_at=data["muted_at"],
            is_muted=is_muted,
            github_issue_url=data["github_issue_url"],)

    def _check_notice_id(self, notice_id):
        errors = []
        if notice_id:
            error = dict(
                field="notice_id",
                code="api_not_implemented",)
            errors.append(error)

        return errors

    def get(self, notice_id):
        errors = self._check_notice_id(notice_id)
        if errors:
            return response.unprocessable_entity(errors=errors)

        notices_cached = self.get_cache("notices")
        if notices_cached is None:
            return response.not_found("No cache for notices.")

        rv = dict(count=0, targets=[])
        notices_activated = [n for n in notices_cached.values() if not n["is_muted"]]
        rv["targets"] = notices_activated
        rv["count"] = len(rv["targets"])
        return jsonify(rv)

    def _check_post_params(self, raw_json_data):
        errors = []
        if raw_json_data:
            # TODO: please check id and time format.
            pass

        return errors

    @security.authenticated
    def post(self):
        json_data = request.get_json(silent=True)
        if not json_data:
            return response.bad_request("Problems parsing JSON.")
        errors = self._check_post_params(json_data)
        if errors:
            return response.unprocessable_entity(errors=errors)

        notices_cached = self.get_cache("notices")
        if not notices_cached:
            notices_cached = {}

        notices_created = notices_cached
        for notice_meta in json_data["targets"]:
            id_str = str(notice_meta["id"])
            if id_str in notices_cached.keys():
                continue
            notices_created[id_str] = self._build_notice(notice_meta)
        if notices_created:
            self.set_cache("notices", notices_created)
            return response.created()
        else:
            return response.ok("Nothing changed.")

    @security.authenticated
    def put(self):
        return response.not_implemented("API hasn't implemented.")

    @security.authenticated
    def delete(self):
        return response.not_implemented("API hasn't implemented.")


def register_api(view, endpoint, url, pk="cname", pk_type="string"):
    view_func = view.as_view(endpoint)
    # e.g. GET,POST /api/mirrors
    app.add_url_rule(url, defaults={pk: None},
                     view_func=view_func, methods=['GET'])
    app.add_url_rule(url, view_func=view_func, methods=['POST'])
    # e.g. GET,PUT,DELETE /api/mirrors/<cname:string>
    app.add_url_rule("{}/<{}:{}>".format(url, pk_type, pk),
                     view_func=view_func, methods=['GET', 'PUT', 'DELETE'])


register_api(Mirrors, "mirrors_api", "/api/mirrors", pk="cname")
register_api(Notices, "notices_api", "/api/notices", pk="notice_id", pk_type="int")
