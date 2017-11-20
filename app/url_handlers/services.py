class URLService:
    """
    Used to parse query string params from a request
    fields -- list of field names that need to be parsed

    """
    def parse_fields_from_request(self, request, fields):
        if isinstance(fields, list):
            fields = {f: f for f in fields}
        if not isinstance(fields, dict):
            return None

        for local_key, incoming_key in fields.items():
            fields[local_key] = request.GET.get(incoming_key)

        return fields
