import { Button, Form, InputGroup, Modal } from 'react-bootstrap';
import { IngredientInputFields } from './IngredientInputFields';
import { PantryIngredient } from '../data/pantry';
import styles from '../styles/PantryIngredientModal.module.css';


interface Props {
    show: boolean;
    title: string;
    buttonText: string;
    pantryIngredient?: PantryIngredient;
    handleClose: () => void;
    handleClick: () => void;
}


export function PantryIngredientModal(
    {show, title, buttonText, pantryIngredient, handleClose, handleClick}
    : Props) {
  
    return (
        <Modal show={show} onHide={handleClose} size="lg">
            <Modal.Header closeButton>
                <Modal.Title>{title}</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Form>
                    <IngredientInputFields ingredient={pantryIngredient? {...pantryIngredient} : null}/>
                    <InputGroup className={`my-3 ${styles.expiration_field}`}>
                        <InputGroup.Text id="expiration-date">
                            expiration date
                        </InputGroup.Text>
                        <Form.Control
                            defaultValue={pantryIngredient ? pantryIngredient.expiration : ""}
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
    );
}
