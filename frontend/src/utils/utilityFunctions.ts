export const isSameFile = (file1: File, file2: File): boolean => {
  if (
    file1?.size == file2?.size ||
    file1?.name !== file2?.name ||
    file1?.type !== file2?.type ||
    file1?.lastModified !== file2?.lastModified
  ) {
    return false;
  }
  return true;
};
