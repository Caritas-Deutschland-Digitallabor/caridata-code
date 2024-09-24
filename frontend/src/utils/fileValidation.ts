import { ParsedData, RequiredColumn } from "@/types/Data";
import { ParseResult } from "papaparse";
import { DataTable } from "dbf-reader/models/dbf-file";

//* Check if the file is a valid CSV or Txt
//* @param content: Content of the file
export const isValidPlainText = (content: ParseResult<string[]>) => {
  if (content.errors.length > 0) {
    return false;
  }
  return true;
};

//* Check if the file is a valid DBF
//* @param content: Content of the file
export const isValidDBF = (content: DataTable) => {
  // check if content exists
  return !!content;
};
//* Check if the required columns are present in the file
//* @param content: Content of the file
//* @param fileType: Type of the file
export const hasRequiredColumns = (
  transformedData: ParsedData,
  requiredColumns: RequiredColumn[],
): [boolean, string[] | undefined] => {
  // 1. Case: Header from file --> check if required mandatory columns are present
  // 2. Case: No header --> check if file has at least same length as required columns
  let hasRequiredColumns: boolean = false;
  let missingColumns: string[] | undefined = undefined;
  if (transformedData.hadHeaderInOriginalFile) {
    // If file has header present we only want to check for mandatory columns
    if (transformedData.hadHeaderInOriginalFile) {
      requiredColumns = requiredColumns.filter(
        (column: RequiredColumn) => column.mandatory,
      );
    }
    missingColumns = requiredColumns
      .filter((column: RequiredColumn) => {
        return !transformedData.headers.includes(column.name);
      })
      .map((column: RequiredColumn) => column.name);
    hasRequiredColumns = missingColumns.length === 0;
  } else {
    hasRequiredColumns =
      transformedData.headers.length >= requiredColumns.length;
    missingColumns = hasRequiredColumns ? [] : undefined;
  }
  return [hasRequiredColumns, missingColumns];
};
