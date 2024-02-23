import { Button, Form, InputGroup, Modal } from 'react-bootstrap';
import { IngredientInputFields } from './IngredientInputFields';
import styles from '../styles/PantryIngredientModal.module.css';


interface Props {
    title: string;
    buttonText: string;
    show: boolean;
    handleClose: () => void;
    handleClick: () => void;
}


export function PantryIngredientModal(
    {show, title, buttonText, handleClose, handleClick}
    : Props) {
  
    return (
        <>
            <Modal show={show} onHide={handleClose} size="lg">
                <Modal.Header closeButton>
                    <Modal.Title>{title}</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Form>
                        <IngredientInputFields/>
                        <InputGroup className={`my-3 ${styles.expiration_field}`}>
                            <InputGroup.Text id="expiration-date">
                                expiration date
                            </InputGroup.Text>
                            <Form.Control
                                type="date"
                            />
                        </InputGroup>
                    </Form>
                </Modal.Body>
                <Modal.Footer>
                    <Button className="custom_button" onClick={handleClick}>
                        {buttonText}
                    </Button>
                </Modal.Footer>
            </Modal>
        </>
    );
}
