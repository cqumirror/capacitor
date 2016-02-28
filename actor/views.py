# -*- coding: utf-8 -*-
from flask import jsonify, request
from flask.views import MethodView

from actor import app
from actor import response
from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()


class Mirrors(MethodView):

    def _mirror(self, data):
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
            comment="",
            has_comment=False,
            size=None,)

    def _check_get_params(self, raw_params):
        errors = []
        if raw_params:
            raise NotImplementedError

        return errors

    def get(self, cname):
        # return list of mirrors
        errors = self._check_get_params(cname)
        if errors:
            return response.unprocessable_entity(errors=errors)
        if cname is None:
            rv = dict(count=0, targets=[])
            mirrors_cache = cache.get("mirrors")
            if mirrors_cache is None:
                return response.not_found("No cache for mirrors.")
            rv["targets"] = mirrors_cache.values()
            rv["count"] = len(rv["targets"])
            return jsonify(rv)
        else:
            mirrors_data = cache.get("mirrors")
            if mirrors_data is None:
                return response.not_found("No cache for mirrors.")
            if cname not in mirrors_data.keys():
                return response.not_found("No such resource.")

            return jsonify(mirrors_data[cname])

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

    def post(self):
        _mirrors = request.get_json(silent=True)
        if not _mirrors:
            return response.bad_request("Problems parsing JSON.")
        errors = self._check_post_params(_mirrors)
        if errors:
            return response.unprocessable_entity(errors=errors)
        mirrors_cache = cache.get("mirrors")
        if not mirrors_cache:
            mirrors_cache = {}
        for mirror in _mirrors:
            cname = mirror["cname"]
            if cname in mirrors_cache.keys():
                continue
            mirrors_cache[cname] = self._mirror(mirror)
        if mirrors_cache:
            cache.set("mirrors", mirrors_cache)
        return response.created()

    def put(self, cname):
        params = request.get_json(silent=True)
        if params is None:
            return response.bad_request("Problems parsing JSON.")
        mirrors_cache = cache.get("mirrors")
        if mirrors_cache is None:
            return response.bad_request("No cache for mirrors.")
        return response.not_implemented("API hasn't implemented.")

    def delete(self, cname):
        return response.not_implemented("API hasn't implemented.")


class Notices(MethodView):

    def _notice(self, data):
        is_muted = True if data["muted_at"] else False
        return dict(
            id=data["id"],
            created_at=data["created_at"],
            muted_at=data["muted_at"],
            is_muted=is_muted,
            github_issue_url=data["github_issue_url"],)

    def _check_get_params(self, raw_params):
        errors = []
        if raw_params:
            raise NotImplementedError

        return errors

    def get(self, id):
        errors = self._check_get_params(None)
        if errors:
            return response.unprocessable_entity(errors=errors)
        rv = dict(count=0, targets=[])
        notices_cache = cache.get("notices")
        if notices_cache is None:
            return response.not_found("No cache for notices.")
        notices_actived = [n for n in notices_cache.values() if not n["is_muted"]]
        rv["targets"] = notices_actived
        rv["count"] = len(rv["targets"])
        return jsonify(rv)

    def _check_post_params(self, raw_json_data):
        errors = []
        if raw_json_data:
            # check id, time format,
            pass

        return errors

    def post(self):
        _notices = request.get_json(silent=True)
        if not _notices:
            return response.bad_request("Problems parsing JSON.")
        errors = self._check_post_params(_notices)
        if errors:
            return response.unprocessable_entity(errors=errors)
        notices_cache = cache.get("notices")
        if not notices_cache:
            notices_cache = {}
        for notice in _notices:
            id_str = str(notice["id"])
            if id_str in notices_cache.keys():
                continue
            notices_cache[id_str] = self._notice(notice)
        if notices_cache:
            cache.set("notices", notices_cache)
        return response.created()

    def put(self):
        return response.not_implemented("API hasn't implemented.")

    def delete(self):
        return response.not_implemented("API hasn't implemented.")


def register_api(view, endpoint, url, pk="cname", pk_type="string"):
    view_func = view.as_view(endpoint)
    app.add_url_rule(url, defaults={pk: None},
                     view_func=view_func, methods=['GET'])
    app.add_url_rule(url, view_func=view_func, methods=['POST'])
    app.add_url_rule("{}/<{}:{}>".format(url, pk_type, pk),
                     view_func=view_func, methods=['GET', 'PUT', 'DELETE'])


register_api(Mirrors, "mirrors_api", "/api/mirrors", pk="cname")
register_api(Notices, "Notices_api", "/api/notices", pk="id", pk_type="int")
