import { IncorrectTypes } from "@/types/Errors";
import { FileSBType } from "@/types/Schema";

// case unsported file type reingeladen Popup fehlermeldung
export const errorInvalidFileType = (fileType: string) => {
  return {
    header: "Fehler beim Dateityp",
    message: `Der Inhalt der Datei entspricht nicht dem eines valides ${fileType.toLocaleUpperCase()}. Bitte überprüfen Sie nochmal!`,
  };
};

export const errorInvalidColumns = (
  missingColumns: string[] | undefined,
  sbType: FileSBType
) => {
  if (!missingColumns) {
    return {
      header: "Fehlende Spalten",
      message: `Datei enthält nicht alle erforderlichen Spalten. Bitte überprüfen Sie den Inhalt der Datei und schauen Sie, ob Sie die richtige Datei (<strong>${sbType}</strong>) ausgewählt haben.`,
    };
  }
  return {
    header: "Fehlende Spalten",
    message: `Folgende erforderliche Spalten fehlen in der Datei: \n<ul>${missingColumns
      .map((item) => `<li>-<strong>${item}</strong></li>`)
      .join(
        ""
      )}</ul>\nBitte überprüfen Sie den Inhalt der Datei und schauen Sie, ob Sie die richtige Datei (<strong>${sbType}</strong>) ausgewählt haben.`,
  };
};

export const errorInvalidTypes = (
  incorrectTypes: IncorrectTypes[],
  sbType: FileSBType
) => {
  return {
    header: "Falsche Spaltenformatierung",
    message: `Folgende Spalten enthalten nicht das erwartete Format: \n${incorrectTypes
      .map(
        (item) =>
          `<ul>
           <li>Spalte: <strong>${item.column}</strong></li>
           <ul>
            <li>- Falsche Werte: <strong>${item.values.join(", ")}</strong></li>
            <li>- Erwartetes Format: <strong>${item.expectedType}</strong></li>
            </ul>
          </ul>Bitte überprüfen Sie den Inhalt der Datei und schauen Sie, ob Sie die richtige Datei (<strong>${sbType}</strong>) ausgewählt haben.`
      )
      .join("")}`,
  };
};

export const errorParsingFile = (error: Error) => {
  return {
    header: "Fehler beim Lesen der Datei",
    message: `${error.message}`,
  };
};

export const errorFileTypeNotSupported = (type: string) => {
  return {
    header: "Dateityp wird nicht unterstützt",
    message: `Dateityp <strong>${type}</strong> wird nicht unterstützt. Bitte laden Sie eine Datei vom Typ <strong>CSV</strong>, <strong>TXT</strong> oder <strong>DBF</strong> hoch.`,
  };
};
