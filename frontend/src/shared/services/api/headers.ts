const APPLICATION_JSON = 'application/json';
const APPLICATION_OCTET_STREAM = 'application/octet-stream';

export const header = {
  GET: {
    Accept: APPLICATION_JSON,
  },
  GET_BLOB: {
    Accept: APPLICATION_OCTET_STREAM,
  },
  POST: {
    Accept: APPLICATION_JSON,
    Content_Type: APPLICATION_JSON,
  },
  POST_FILE: {
    Accept: APPLICATION_JSON,
    Content_Type: APPLICATION_JSON,
  },
  PUT: {
    Accept: APPLICATION_JSON,
    Content_Type: APPLICATION_JSON,
  },
  DELETE: {
    Accept: APPLICATION_JSON,
    Content_Type: APPLICATION_JSON,
  },
  PATCH: {
    Accept: APPLICATION_JSON,
    Content_Type: 'application/jsonpatch+json',
  },
};
