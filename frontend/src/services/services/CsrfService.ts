/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CancelablePromise } from '../core/CancelablePromise';
import type { BaseHttpRequest } from '../core/BaseHttpRequest';
export class CsrfService {
    constructor(public readonly httpRequest: BaseHttpRequest) {}
    /**
     * Send Csrf Token
     * @returns void
     * @throws ApiError
     */
    public sendCsrfToken(): CancelablePromise<void> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/csrf/',
        });
    }
}
