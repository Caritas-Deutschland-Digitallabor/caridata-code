/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CheckTokenOut } from '../models/CheckTokenOut';
import type { InvitationOut } from '../models/InvitationOut';
import type { CancelablePromise } from '../core/CancelablePromise';
import type { BaseHttpRequest } from '../core/BaseHttpRequest';
export class InvitationsService {
    constructor(public readonly httpRequest: BaseHttpRequest) {}
    /**
     * Send Invitation
     * Send an invitation to a representative of an organisation to upload data.
     *
     * Args:
     * organisation (Organisation): Organisation instance
     * token (str): Invitation token
     * db_session (AsyncSession): AsyncSession instance
     * @param organisationId ID der Organisation
     * @returns any Successful Response
     * @throws ApiError
     */
    public sendInvitation(
        organisationId: number,
    ): CancelablePromise<any> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/invitations/send/{organisation_id}',
            path: {
                'organisation_id': organisationId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * List Invitations
     * List all invitations.
     *
     * Args:
     * db_session (AsyncSession): AsyncSession instance
     * @returns InvitationOut Successful Response
     * @throws ApiError
     */
    public listInvitations(): CancelablePromise<Array<InvitationOut>> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/invitations/',
        });
    }
    /**
     * Check Invitation Token
     * Check if an invitation token is valid.
     *
     * Args:
     * db_session (AsyncSession): AsyncSession instance
     * token (str): Invitation token
     * @param token Einladungs-Token
     * @returns CheckTokenOut Successful Response
     * @throws ApiError
     */
    public checkInvitationToken(
        token: string,
    ): CancelablePromise<CheckTokenOut> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/invitations/check-token/{token}',
            path: {
                'token': token,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
