import proto.application.application_pb2 as application_pb
from manager.base_manager import BaseManager
from dao.application.application import ApplicationDB


class ApplicationManager(BaseManager):

    @property
    def application_da(self):
        if not self._application_da:
            self._application_da = ApplicationDB()
        return self._application_da

    def _init(self, *argrs, **kargs):
        self._application_da = None

    def create_application(self, req):
        application = self.create_obj(application_pb.Application)
        application.name = req.name
        return application

    def list_applications(self, req):
        applications = self.application_da.list_applications_with_create_time_order(
            req.last_create_time)
        return applications

    def add_or_update_application(self, application):
        if not application:
            return
        super().update_obj(application)
        self.application_da.add_or_update_application(application)
