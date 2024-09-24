/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { InvitationOut } from './InvitationOut';
export type OrganisationOut = {
    id: number;
    name?: (string | null);
    email?: (string | null);
    invitation_email?: (string | null);
    invitations?: (Array<InvitationOut> | null);
    created_at: string;
    updated_at?: (string | null);
    deprecated_at?: (string | null);
};
