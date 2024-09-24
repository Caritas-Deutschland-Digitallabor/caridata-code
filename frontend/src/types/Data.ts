export type FileType =
  | { type: "dbf"; subType: undefined }
  | { type: "plainText"; subType: "csv" }
  | { type: "plainText"; subType: "tsv" };
export type Row = {
  [key: string]: string;
};
export type ParsedData = {
  headers: string[];
  rows: Row[];
  hadHeaderInOriginalFile: boolean;
};
export type RequiredColumn = {
  name: string;
  mandatory: boolean;
};
