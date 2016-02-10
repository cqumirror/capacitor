# -*- coding: utf-8 -*-
from actor import app
from flask import jsonify, request, abort, url_for
from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()

TIME_OLD_FORMAT = "%Y%m%d %H:%M:%S"
TIME_NEW_FORMAT = "%Y-%m-%d %H:%M:%S"
TIME_UNKNOWN = "????-??-?? ??:??:??"


@app.route("/api/mirrors", methods=["GET", "POST", "PUT", "DELETE"])
def mirrors():
    if request.method == "GET":
        rv = dict(count=0, targets=[], states_url=url_for("states"))

        mirrors_data = cache.get("mirrors")
        if mirrors_data is None:
            cache.set("mirrors", {})
            return jsonify(rv)

        rv["targets"] = mirrors_data.values()
        rv["count"] = len(rv["targets"])
        return jsonify(rv)

    if request.method == "POST":
        import json
        with open("data_local/mirrors.json", "r") as json_file:
            mirrors_data = json.load(json_file)

        mirrors_data_f = {}
        for v in mirrors_data:
            target = dict(
                cname=v["cname"],
                full_name=v["full_name"],
                url="{}://{}{}".format(v["protocol"], v["host"], v["path"]),
                help_url=v["help"],
                state_url=url_for("states", cname=v["cname"]),
                created_at=TIME_UNKNOWN,
                upstream_url="",)
            mirrors_data_f[v["cname"]] = target
        cache.set("mirrors", mirrors_data_f)
        return jsonify(cache.get("mirrors"))

    abort(501)


@app.route("/api/mirrors/states")
@app.route("/api/mirrors/states/cname:<cname>",
           methods=["GET", "POST", "PUT", "DELETE"])
def states(cname=None):
    rv = dict(count=0, targets=[])
    target = dict(
        sync_code=500,
        last_sync=TIME_UNKNOWN,
        comment="",
        size="unknown",)
    rv["targets"].append(target)
    rv["count"] = len(rv["targets"])
    return jsonify(rv)

#
# def format_size(size):
#     return round(float(size) / (1024 * 1024), 2)
#
#
# def prepare_mirrors_status(target):
#     """Update mirrors' last_sync, size, status, message property."""
#     mirror_log = '.'.join([target["name"], "log"])
#     mirror_log_path = os.path.join(app.config["SYNC_LOG_DIR"], mirror_log)
#     try:
#         with open(mirror_log_path, 'r') as f:
#             lines = f.readlines()
#
#             # 0: yyyyMMdd 1: HH:mm:ss
#             # 2: SyncStart | SyncSuccd | SyncError | SyncCompt
#             # 3: Size or Return code
#             last_line_values = lines[-1].rstrip().split(" - ")
#             second_last_values = lines[-2].rstrip().split(" - ")
#             stage = last_line_values[2]
#
#             if stage == "SyncCompt":
#                 time = ' '.join([last_line_values[0], last_line_values[1]])
#                 target["last_sync"] = datetime.strptime(time, TIME_OLD_FORMAT).strftime(TIME_NEW_FORMAT)
#                 target["size"] = ''.join([str(format_size(int(last_line_values[3]))), 'G'])   # KB to GB
#                 if second_last_values[-2] == "SyncError":
#                     error_code = second_last_values[3]
#                     error_message = get_error_message(error_code)
#                     target["message"] = \
#                         "Error code: {} - {}".format(error_code, error_message)
#                     target["status"] = 400
#                 else:
#                     target["message"] = ''
#                     target["status"] = 200
#
#             if stage == "SyncStart":
#                 time = ' '.join([second_last_values[0], second_last_values[1]])
#                 target["last_sync"] = datetime.strptime(time, TIME_OLD_FORMAT).strftime(TIME_NEW_FORMAT)
#                 target["size"] = ''.join([str(format_size(int(last_line_values[3]))), 'G'])   # KB to GB
#                 target["message"] = ''
#                 target["status"] = 100
#     except IOError:
#         target["message"] = "Fail to read sync log file."
#         target["status"] = 500
#     except IndexError:
#         target["message"] = "Invalid sync log format."
#         target["status"] = 500
#
#
# @app.route("/api/mirrors/status")
# def mirrors_states():
#     res = dict(count=0, targets=[])
#     for mirror in mirrors:
#         # Only name in row
#         target = dict(
#             name=mirror.name,
#             last_sync=TIME_UNKNOWN,
#             size="unknown",
#             status=500,
#             message=''
#         )
#         prepare_mirrors_status(target)
#         res["targets"].append(target)
#     res["count"] = len(res["targets"])
#     return jsonify(res)
#
#
# @app.route("/api/mirrors/notices")
# def get_mirrors_notices():
#     """Show the last notices."""
#     res = dict(count=0, targets=[])
#
#     for notice in notices:
#         time_created_f = notice.created.strftime(TIME_NEW_FORMAT)
#         notice_f = dict(
#             created_at=time_created_f,
#             notice=notice.content,
#             level=notice.level
#         )
#         res["targets"].append(notice_f)
#     res["count"] = len(res["targets"])
#     return jsonify(res)
#
#
# def format_version(version):
#     if '-' not in version:
#         return version
#
#     # target format: 7.1 (x86_64, Minimal, ...)
#     values = version.split('-')
#     version_f = "{} ({})".format(values[0], ", ".join(values[1:]))
#     return version_f
#
#
# @app.route("/api/mirrors/oses")
# def get_mirrors_oses():
#     res = dict(count=0, targets=[])
#     os_names = [row.name for row in query.all()]
#
#     for os_name in os_names:
#         # fetch all versions of the os
#         os_versions = MirrorsResources.query.\
#             filter_by(type="os", name=os_name, status=0).all()
#
#         # prepare the os object
#         o_s_f = dict(name=os_name,
#                      fullname='',
#                      type="os",
#                      url='',
#                      versions=[],
#                      count=0)
#
#         for (idx, o_s) in enumerate(os_versions):
#             # init the os object
#             if idx == 0:
#                 o_s_f["fullname"] = o_s.fullname
#                 o_s_f["url"] =\
#                     ''.join([o_s.protocol, "://", o_s.host, o_s.dir])
#
#             # add new version of the os
#             os_version_f = format_version(o_s.version)
#             os_version_url =\
#                 ''.join([o_s.protocol, "://", o_s.host, o_s.path])
#             version = dict(version=os_version_f, url=os_version_url)
#             o_s_f["versions"].append(version)
#         # update count of the os's version object
#         o_s_f["count"] = len(o_s_f["versions"])
#         res["targets"].append(o_s_f)
#     res["count"] = len(res["targets"])
#     return jsonify(res)
#
#
# @app.route("/api/mirrors/osses")
# def get_mirrors_osses():
#     """Retrun list of some Open Source Softwares."""
#     res = dict(count=0, targets=[])
#
#     for oss_name in oss_names:
#         # fetch all versions of the oss
#         oss_versions = MirrorsResources.query.\
#             filter_by(type="oss", name=oss_name, status=0).all()
#
#         # prepare the oss object
#         oss_f = dict(name=oss_name, fullname='', type="oss", url='', versions=[], count=0)
#
#         for (idx, oss) in enumerate(oss_versions):
#             # init the oss object
#             if idx == 0:
#                 oss_f["fullname"] = oss.fullname
#                 oss_f["url"] = ''.join([oss.protocol, "://", oss.host, oss.dir])
#
#             # add new version of the oss
#             oss_version_f = format_version(oss.version)
#             oss_version_url = ''.join([oss.protocol, "://", oss.host, oss.path])
#             version = dict(version=oss_version_f, url=oss_version_url)
#             oss_f["versions"].append(version)
#         # update count of the os's version object
#         oss_f["count"] = len(oss_f["versions"])
#         res["targets"].append(oss_f)
#     res["count"] = len(res["targets"])
#     return jsonify(res)


@app.after_request
def custom_headers(res):
    res.headers["Server"] = app.config["APP_NAME"]
    return res
