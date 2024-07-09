import { Button, Form, Modal } from 'react-bootstrap';
import { IngredientInputFields } from './IngredientInputFields';
import { ShoppingListItem } from '../types/interfaces';
import { useEffect, useState } from 'react';

interface Props {
    show: boolean;
    title: string;
    buttonText: string;
    shoppingListItem?: ShoppingListItem;
    handleClose: () => void;
    handleClick: (shoppingListItem: ShoppingListItem) => void;
}


export function ShoppingItemModal(
    {show, title, buttonText, shoppingListItem, handleClose, handleClick}: Props) {

    const [shoppingItem, setShoppingItem] = useState<ShoppingListItem | null>(null);

    useEffect(() => {
        if (shoppingListItem) {
            setShoppingItem(shoppingListItem);
        }
    }, [shoppingListItem]);

    return (
        <Modal show={show} onHide={handleClose} size="lg">
            <Modal.Header closeButton>
                <Modal.Title>{title}</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Form>
                    <IngredientInputFields
                        handleChange={(ingredient) => setShoppingItem(ingredient)}
                    />
                </Form>
            </Modal.Body>
            <Modal.Footer>
                <Button
                    className="custom_button"
                    onClick={shoppingItem? () => handleClick(shoppingItem) : () => {}}
                >
                    {buttonText}
                </Button>
            </Modal.Footer>
        </Modal>
    );
}
