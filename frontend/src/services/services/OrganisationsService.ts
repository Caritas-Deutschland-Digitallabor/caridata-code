/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { OrganisationOut } from '../models/OrganisationOut';
import type { CancelablePromise } from '../core/CancelablePromise';
import type { BaseHttpRequest } from '../core/BaseHttpRequest';
export class OrganisationsService {
    constructor(public readonly httpRequest: BaseHttpRequest) {}
    /**
     * List Organisations
     * @param all Auch gelöschte Organisationen anzeigen
     * @returns OrganisationOut Successful Response
     * @throws ApiError
     */
    public listOrganisations(
        all: boolean = false,
    ): CancelablePromise<Array<OrganisationOut>> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/organisations/',
            query: {
                'all': all,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Organisation By Id
     * @param organisationId ID der Organisation
     * @returns OrganisationOut Successful Response
     * @throws ApiError
     */
    public getOrganisationById(
        organisationId: number,
    ): CancelablePromise<OrganisationOut> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/organisations/{organisation_id}/',
            path: {
                'organisation_id': organisationId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Synchronize Organisations
     * @returns void
     * @throws ApiError
     */
    public synchronizeOrganisations(): CancelablePromise<void> {
        return this.httpRequest.request({
            method: 'PATCH',
            url: '/organisations/synchronisieren/',
        });
    }
    /**
     * Upsert Organisation Invitation Email
     * @param organisationId ID der Organisation
     * @param requestBody
     * @returns OrganisationOut Successful Response
     * @throws ApiError
     */
    public upsertOrganisationInvitationEmail(
        organisationId: number,
        requestBody: string,
    ): CancelablePromise<OrganisationOut> {
        return this.httpRequest.request({
            method: 'PATCH',
            url: '/organisations/{organisation_id}/invitation-email/',
            path: {
                'organisation_id': organisationId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
