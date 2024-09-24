/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { SchemaOut } from '../models/SchemaOut';
import type { CancelablePromise } from '../core/CancelablePromise';
import type { BaseHttpRequest } from '../core/BaseHttpRequest';
export class VariablesService {
    constructor(public readonly httpRequest: BaseHttpRequest) {}
    /**
     * List Variables
     * @param variableName Name of the variable
     * @param source Source of the variable
     * @returns SchemaOut Successful Response
     * @throws ApiError
     */
    public listVariables(
        variableName?: (string | null),
        source?: 'sbkont' | 'sbkern1' | 'stelle' | 'sbveran' | 'sbkern2',
    ): CancelablePromise<Array<SchemaOut>> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/variables/',
            query: {
                'variable_name': variableName,
                'source': source,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
