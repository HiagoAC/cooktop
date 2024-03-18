import { Alert } from 'react-bootstrap';


export interface Props {
    successCondition: boolean | null;
    successMessage?: string;
    failMessage?: string;
}


export function RequestAlert({
        successCondition,
        successMessage = 'Saved!',
        failMessage = 'Request failed.'
    }: Props) {

    return (
        <>
            { successCondition? (
                <Alert variant="success" className="m-4">
                    {successMessage}
                </Alert>
            ) : successCondition === false? (
                <Alert variant="danger" className="mb-4">
                    {failMessage}
                </Alert>
            ) : (<></>)}
        </>
    )
}
