import { Button, Form, Modal } from 'react-bootstrap';
import { IngredientInputFields } from './IngredientInputFields';
import { ShoppingListItem } from '../types/interfaces';
import { useEffect, useState } from 'react';

interface Props {
    show: boolean;
    title: string;
    buttonText: string;
    mode: 'create' | 'edit';
    shoppingListItem?: ShoppingListItem;
    handleClose: () => void;
    handleClick: (shoppingListItem: ShoppingListItem | Omit<ShoppingListItem, 'id'>) => void;
}


export function ShoppingItemModal(
    {show, title, buttonText, mode, shoppingListItem, handleClose, handleClick}: Props) {

    const [shoppingItem, setShoppingItem] = useState<
        ShoppingListItem | Omit<ShoppingListItem, 'id'> | null>(null);

useEffect(() => {
        console.log('Entering use effect to set shopping item')
        if (shoppingListItem) {
            console.log('Setting shopping item')
            setShoppingItem(shoppingListItem);
            console.log(shoppingListItem);
            console.log(shoppingItem);
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
                        ingredient={shoppingItem? shoppingItem as ShoppingListItem : null}
                        mode={mode}
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
