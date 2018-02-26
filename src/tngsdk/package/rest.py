#  Copyright (c) 2015 SONATA-NFV, 5GTANGO, UBIWHERE, Paderborn University
# ALL RIGHTS RESERVED.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Neither the name of the SONATA-NFV, 5GTANGO, UBIWHERE, Paderborn University
# nor the names of its contributors may be used to endorse or promote
# products derived from this software without specific prior written
# permission.
#
# This work has been performed in the framework of the SONATA project,
# funded by the European Commission under Grant number 671517 through
# the Horizon 2020 and 5G-PPP programmes. The authors would like to
# acknowledge the contributions of their colleagues of the SONATA
# partner consortium (www.sonata-nfv.eu).
#
# This work has also been performed in the framework of the 5GTANGO project,
# funded by the European Commission under Grant number 761493 through
# the Horizon 2020 and 5G-PPP programmes. The authors would like to
# acknowledge the contributions of their colleagues of the SONATA
# partner consortium (www.5gtango.eu).
import logging
import os
from flask import Flask
from flask_restplus import Resource, Api, fields
from werkzeug.contrib.fixers import ProxyFix
from werkzeug.datastructures import FileStorage
from tngsdk.package.packager import PM


LOG = logging.getLogger(os.path.basename(__file__))


app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app,
          version="1.0",
          title='5GTANGO tng-package API',
          description="5GTANGO tng-package REST API " +
          "to package/unpacke NFV packages.")


def serve_forever(args, debug=True):
    """
    Start REST API server. Blocks.
    """
    # TODO replace this with WSGIServer for better performance
    app.run(host=args.service_address,
            port=args.service_port,
            debug=debug)


packages_parser = api.parser()
packages_parser.add_argument("package",
                             location="files",
                             type=FileStorage,
                             required=True,
                             help="Uploaded package file")
packages_parser.add_argument("callback_url",
                             location="form",
                             required=False,
                             default=None,
                             help="URL called after unpackaging (optional)")
packages_parser.add_argument("layer",
                             location="form",
                             required=False,
                             default=None,
                             help="Layer tag to be unpackaged (optional)")
packages_parser.add_argument("format",
                             location="form",
                             required=False,
                             default="eu.5gtango",
                             help="Package format (optional)")

packages_model = api.model("Packages", {
    "package_process_uuid": fields.String(
        description="UUID of started unpackaging process.",
        required=True
    )
})


def on_unpackaging_done(args):
    """
    Callback function for packaging procedure.
    """
    LOG.info("on_unpackaging_done")
    LOG.warning("not implemented")
    # TODO: Do callback url request


def on_packaging_done(args):
    """
    Callback function for packaging procedure.
    """
    LOG.info("on_packaging_done")
    LOG.warning("not implemented")


@api.route("/packages")
class Package(Resource):
    """
    Endpoint for unpackaging.
    """
    @api.expect(packages_parser)
    @api.marshal_with(packages_model)
    @api.response(200, "Successfully started unpackaging.")
    @api.response(400, "Bad package: Could not unpackage given package.")
    def post(self, **kwargs):
        args = packages_parser.parse_args()
        # TODO replace package data with local path to file
        print(args["package"])
        print(args["callback_url"])
        p = PM.new_packager(args)  # TODO pass args to packager
        p.unpackage(callback_func=on_unpackaging_done)
        return {"package_process_uuid": p.uuid}


@api.route("/projects")
class Project(Resource):
    """
    Endpoint for package creation.
    """
    def post(self):
        LOG.warning("endpoint not implemented")
        p = PM.new_packager(None)
        p.package(callback_func=on_packaging_done)
        return "not implemented", 501