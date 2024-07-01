import { Modal, Button } from 'react-bootstrap';

interface Props {
    show: boolean;
    onHide: () => void;
}


export function UpdateListsFromMealPlanModal({ show, onHide }: Props) {
    return (
        <Modal show={show} onHide={onHide} bg="warning">
            <Modal.Header>
                <Modal.Title>{'Alert!'}</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <h5>{'Have you finished editing this meal plan?'}</h5>
                <p>{'You will have to update pantry and shopping list manually\
                    if you make changes to this meal plan after clicking Yes.'}</p>
            </Modal.Body>
            <Modal.Footer className="d-flex justify-content-end">
                <Button
                    onClick={onHide}
                    variant="success"
                >
                    {'Yes'}
                </Button>
                <Button
                    onClick={onHide}
                    variant="danger"
                >
                    {'No'}
                </Button>
            </Modal.Footer>
        </Modal>
    )
}
