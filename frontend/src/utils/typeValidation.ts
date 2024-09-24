import { CategoryOut } from "@/services/models/CategoryOut";
import { SchemaOut } from "@/services/models/SchemaOut";
import { ParsedData } from "@/types/Data";
import { IncorrectTypes, RequiredTypes } from "@/types/Errors";
import moment from "moment";

const isUndefined = (value: any) => {
  return value === "" || value === null || value === "NA";
};

export const hasCorrectTypes = (
  transformedData: ParsedData,
  requiredTypes: RequiredTypes,
  schema: SchemaOut[],
): [boolean, IncorrectTypes[]] => {
  let incorrectTypes: IncorrectTypes[] = [];

  // Define a map of type validators
  const typeValidators: {
    [key: string]: (value: any, key?: string) => boolean;
  } = {
    integer: isValidNumber,
    boolean: isValidBoolean,
    categorical: (value, key) =>
      isValidCategories(
        value,
        schema.find((s) => s.name === key)?.categories || [],
      ),
    date: isValidDate,
    float: isValidFloat,
  };

  // Validate each row
  for (let row of transformedData.rows) {
    for (let key in row) {
      const requiredType = requiredTypes[key];
      const validator = typeValidators[requiredType];

      if (validator && !validator(row[key], key)) {
        incorrectTypes.push({
          column: key,
          values: transformedData.rows.map((r) => r[key]),
          expectedType: requiredType,
        });
        return [false, incorrectTypes];
      }
    }
  }

  return [true, incorrectTypes];
};

export const isValidBoolean = (value: any) => {
  //Todo: fix this with mandatory value
  if (isUndefined(value)) {
    return true;
  }
  if (typeof value === "boolean") {
    return true;
  }
  return (
    value.toLowerCase() === "true" ||
    value.toLowerCase() === "false" ||
    value === "1" ||
    value === "0" ||
    value === "F" ||
    value === "T"
  );
};

export const isGermanFloat = (value: string) => {
  const germanFloatPattern = /^(\d{1,3})(\.\d{3})*(,\d+)?$/;
  return germanFloatPattern.test(value);
};

export const parseGermanFloat = (value: string) => {
  let normalizedValue = value.replace(/\./g, "").replace(",", ".");
  return parseFloat(normalizedValue);
};

export const isValidNumber = (value: any) => {
  //Todo: fix this with mandatory value
  if (isUndefined(value)) {
    return true;
  }
  return !isNaN(Number(value));
};

export const isValidFloat = (value: any) => {
  //Todo: fix this with mandatory value
  if (isUndefined(value)) {
    return true;
  }
  if (typeof value === "number") {
    return Number.isFinite(value);
  }
  if (typeof value === "string") {
    value = value.trim();
    const parsed = isGermanFloat(value)
      ? parseGermanFloat(value)
      : parseFloat(value);
    return (
      !isNaN(parsed) &&
      isFinite(parsed) &&
      (parsed.toString() === value || isGermanFloat(value))
    );
  }
  // All other types (boolean, object, array, null, etc.) are not floats
  return false;
};

export const isValidCategories = (
  value: any,
  categoryDefinition: CategoryOut[],
) => {
  //Todo: fix this with mandatory value
  if (isUndefined(value)) {
    return true;
  }
  if (typeof value === "boolean") {
    return false;
  }
  if (
    categoryDefinition
      .map((category) => {
        return category.value;
      })
      .includes(value.toString())
  ) {
    return true;
  } else {
    return false;
  }
};

export const isValidDate = (value: any) => {
  //Todo: fix this with mandatory value
  if (isUndefined(value)) {
    return true;
  }
  const formats = [
    moment.ISO_8601,
    "DD.MM.YYYY",
    "MM/DD/YYYY",
    "YYYY-MM-DD",
    "DD/MM/YYYY",
    "MM-DD-YYYY",
  ];
  return formats.some((format) => moment(value, format, true).isValid());
};
