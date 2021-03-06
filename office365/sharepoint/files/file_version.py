from office365.runtime.client_object import ClientObject
from office365.runtime.queries.delete_entity_query import DeleteEntityQuery
from office365.runtime.resource_path_service_operation import ResourcePathServiceOperation


class FileVersion(ClientObject):
    """Represents a version of a File object."""

    @property
    def url(self):
        """Gets a value that specifies the relative URL of the file version based on the URL for the site or subsite."""
        return self.properties.get("Url", None)

    @property
    def version_label(self):
        """Gets a value that specifies the implementation specific identifier of the file."""
        return self.properties.get("VersionLabel", None)

    @property
    def is_current_version(self):
        """Gets a value that specifies whether the file version is the current version."""
        return self.properties.get("IsCurrentVersion", None)

    @property
    def checkin_comment(self):
        """Gets a value that specifies the check-in comment."""
        return self.properties.get("CheckInComment", None)

    def delete_object(self):
        """Deletes the fields."""
        qry = DeleteEntityQuery(self)
        self.context.add_query(qry)
        self.remove_from_parent_collection()
        return self

    def set_property(self, name, value, persist_changes=True):
        super(FileVersion, self).set_property(name, value, persist_changes)
        if self._resource_path is None:
            if name == "ID":
                self._resource_path = ResourcePathServiceOperation(
                    "GetById",
                    [value],
                    self._parent_collection.resource_path)
