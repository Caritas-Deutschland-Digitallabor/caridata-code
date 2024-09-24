/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CategoryOut } from './CategoryOut';
export type SchemaOut = {
    id: string;
    name: string;
    source: string;
    text: string;
    type: string;
    value_from?: (string | null);
    value_to?: (string | null);
    technical_mandatory: boolean;
    mandatory: boolean;
    file_position: number;
    missing?: (string | null);
    created_at: string;
    deprecated_at?: (string | null);
    categories?: (Array<CategoryOut> | null);
};
