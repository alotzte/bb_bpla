type EncodeURIComponentArgs = string | number | boolean;
type ParamsSerializerParams = Record<
  string,
  EncodeURIComponentArgs | EncodeURIComponentArgs[]
>;

export const paramsSerializer = (params?: ParamsSerializerParams) => {
  if (!params || Object.keys(params ?? {}).length === 0) {
    return '';
  }

  const query = Object.keys(params)
    .map((key) => {
      const value = params[key];
      if (Array.isArray(value)) {
        return value
          .map(
            (arrValue) =>
              `${encodeURIComponent(key)}=${encodeURIComponent(arrValue)}`
          )
          .join('&');
      } else {
        return `${encodeURIComponent(key)}=${encodeURIComponent(value)}`;
      }
    })
    .join('&');

  return query;
};
