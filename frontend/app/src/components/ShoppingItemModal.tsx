import { Button, Form, Modal } from 'react-bootstrap';
import { IngredientInputFields } from './IngredientInputFields';
import { addItemToList } from '../api/shoppingListApi';
import { ShoppingListItem } from '../types/interfaces';
import { useState } from 'react';


interface Props {
    show: boolean;
    handleClose: () => void;
}


export function ShoppingItemModal(
    {show, handleClose}
    : Props) {
    
    const [shoppingItem, setShoppingItem] = useState<ShoppingListItem | null>(null);


    const addItem = () => {
        if (!shoppingItem) {
            return;
        }
        addItemToList(shoppingItem).then(res => {
            console.log(res);
            handleClose();
        });
    };

    return (
        <Modal show={show} onHide={handleClose} size="lg">
            <Modal.Header closeButton>
                <Modal.Title>{"Add a new item"}</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Form>
                    <IngredientInputFields
                        handleChange={(ingredient) => setShoppingItem({
                            name: ingredient.name,
                            quantity: ingredient.quantity,
                            unit: ingredient.display_unit
                        })}
                    />
                </Form>
            </Modal.Body>
            <Modal.Footer>
                <Button className="custom_button" onClick={addItem}>
                    {"Save"}
                </Button>
            </Modal.Footer>
        </Modal>
    );
}
