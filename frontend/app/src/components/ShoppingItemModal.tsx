import { Button, Form, Modal } from 'react-bootstrap';
import { IngredientInputFields } from './IngredientInputFields';
import { ShoppingItem } from '../data/shopping_list';


interface Props {
    show: boolean;
    title: string;
    buttonText: string;
    shoppingItem?: ShoppingItem;
    handleClose: () => void;
    handleClick: () => void;
}


export function ShoppingItemModal(
    {show, title, buttonText, shoppingItem, handleClose, handleClick}
    : Props) {
  
    return (
        <>
            <Modal show={show} onHide={handleClose} size="lg">
                <Modal.Header closeButton>
                    <Modal.Title>{title}</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Form>
                        <IngredientInputFields ingredient={shoppingItem? {...shoppingItem} : null}/>
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
