export const mimeTypeRule = (value: File) => {
  const allowedMimeTypes = [
    "text/csv",
    "application/csv",
    "text/x-csv",
    "text/plain",
    "application/dbf",
    "application/x-dbf",
    "application/vnd.dbf",
    "application/vnd.dbf",
    "",
  ];
  if (!allowedMimeTypes.includes(value.type)) {
    return "Dateityp " + value.type + "  nicht erlaubt";
  }
  return true;
};
