# -*- coding: utf-8 -*-
from actor import app
from flask import jsonify, request, abort, url_for, make_response
from flask.views import MethodView
import errors

from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()

TIME_OLD_FORMAT = "%Y%m%d %H:%M:%S"
TIME_NEW_FORMAT = "%Y-%m-%d %H:%M:%S"
TIME_UNKNOWN = "????-??-?? ??:??:??"


class Mirrors(MethodView):

    def _build_url(self, protocol, host, path):
        return "{}://{}{}".format(protocol, host, path)

    def get(self, cname):
        # return list of mirrors
        if cname is None:
            rv = dict(count=0, targets=[],
                      states_url=url_for("states_api", _external=True))
            mirrors_cache = cache.get("mirrors")
            if mirrors_cache is None:
                return errors.not_found("No cache for mirrors")
            rv["targets"] = mirrors_cache.values()
            rv["count"] = len(rv["targets"])
            return jsonify(rv)
        else:
            mirrors_data = cache.get("mirrors")
            if mirrors_data is None:
                return errors.not_found("No cache for mirrors")
            if cname not in mirrors_data.keys():
                return errors.not_found("No such resource")

            return jsonify(mirrors_data[cname])

    def _check_params(self, raw_data):
        errors_list = []
        fields = ["cname", "full_name", "protocol", "host", "path",
                  "help", "created_at", "upstream_url", ]
        fields_missing = [key for key in fields
                          if key not in raw_data.keys()]
        if fields_missing:
            error = dict(
                resource="mirrors/{}".format(raw_data["cname"]),
                fields=fields_missing,
                code="missing_field",)
            errors_list.append(error)
        return errors_list

    def post(self):
        mirrors_list = request.get_json(silent=True)
        if mirrors_list is None:
            return errors.bad_request("Problems parsing JSON")
        mirrors_cache = cache.get("mirrors")
        if mirrors_cache is None:
            mirrors_cache = {}
        errors_list = []
        for e in mirrors_list:
            error = self._check_params(e)
            if error:
                errors_list += error
                continue
            if e["cname"] in mirrors_cache.keys():
                continue
            target = dict(
                cname=e["cname"],
                full_name=e["full_name"],
                url=self._build_url(e["protocol"], e["host"], e["path"]),
                help_url=e["help"],
                state_url=url_for("states_api", cname=e["cname"],
                                  _external=True, _method="GET"),
                created_at=e["created_at"],
                upstream_url=e["upstream_url"],)
            mirrors_cache[e["cname"]] = target
        if mirrors_cache:
            cache.set("mirrors", mirrors_cache)

        if errors_list:
            return errors.unprocessable_entity(errors=errors_list)
        else:
            return make_response("Created", 201)

    def put(self):
        return errors.not_implemented()

    def delete(self):
        return errors.not_implemented()


class MirrorStates(MethodView):

    def get(self, cname):
        rv = dict(count=0, targets=[])
        target = dict(
            sync_code=500,
            last_sync=TIME_UNKNOWN,
            comment="",
            size="unknown",)
        rv["targets"].append(target)
        rv["count"] = len(rv["targets"])
        return jsonify(rv)

    def post(self):
        return errors.not_implemented()


class Notices(MethodView):
    pass


def register_api(view, endpoint, url, pk, pk_type="string"):
    view_func = view.as_view(endpoint)
    app.add_url_rule(url, defaults={pk: None},
                     view_func=view_func, methods=['GET'])
    app.add_url_rule(url, view_func=view_func, methods=['POST'])
    app.add_url_rule("{}{}:<{}:{}>".format(url, pk, pk_type, pk),
                     view_func=view_func, methods=['GET', 'PUT', 'DELETE'])


register_api(Mirrors, "mirrors_api", "/api/mirrors/", pk="cname")
register_api(MirrorStates, "states_api", "/api/mirrors/states/", pk="cname")
