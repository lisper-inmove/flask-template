import api.application_api_pb2 as application_api_pb
from ctrl.base_ctrl import BaseCtrl
from manager.application.application import ApplicationManager
from submodules.utils.idate import IDate


class ApplicationCtrl(BaseCtrl):

    def register(self):
        req = self.get_request_obj(application_api_pb.ApplicationRegisterRequest)
        manager = ApplicationManager()
        application = manager.create_application(req)
        manager.add_or_update_application(application)
        return self.empty_data_response()

    def list(self):
        req = self.get_request_obj(application_api_pb.ApplicationListRequest)
        if not req.last_create_time:
            req.last_create_time = IDate.now_timestamp()
        manager = ApplicationManager()
        applications = manager.list_applications(req)
        return self.__convert_application_to_ApplicationQueryResponses(applications)

    def __convert_application_to_ApplicationQueryResponse(self, application):
        obj = application_api_pb.ApplicationQueryResponse()
        obj.id = application.id
        obj.name = application.name
        obj.create_time = application.create_time_sec
        return obj

    def __convert_application_to_ApplicationQueryResponses(self, applications):
        result = application_api_pb.ApplicationListResponse()
        for a in applications:
            result.applications.add().CopyFrom(
                self.__convert_application_to_ApplicationQueryResponse(a))
        return result
