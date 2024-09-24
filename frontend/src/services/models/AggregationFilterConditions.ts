/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type AggregationFilterConditions = {
    field: string;
    value: (string | number);
    condition: AggregationFilterConditions.condition;
};
export namespace AggregationFilterConditions {
    export enum condition {
        _ = '=',
        _ = '!=',
        _ = '>',
        _ = '<',
        _ = '>=',
        _ = '<=',
        IS_NOT = 'IS NOT',
        IS = 'IS',
    }
}
