import {useEffect, useState} from 'react';
import { Button, Form, InputGroup, Modal } from 'react-bootstrap';
import { IngredientInputFields } from './IngredientInputFields';
import { Ingredient, PantryIngredient } from '../types/interfaces';
import styles from '../styles/PantryIngredientModal.module.css';


interface Props {
    show: boolean;
    title: string;
    buttonText: string;
    mode: 'create' | 'edit';
    pantryIngredientInit?: PantryIngredient;
    handleClose: () => void;
    handleClick: (pantryIngredient: PantryIngredient | Omit<
        PantryIngredient, 'id'>) => void;
}


export function PantryIngredientModal(
    {show, title, buttonText, mode, pantryIngredientInit, handleClose, handleClick}
    : Props) {
    const [ingredient, setIngredient] = useState<
        Ingredient | Omit<Ingredient, 'id'> | null>(null);
    const [expiration, setExpiration] = useState<string>("");
    
    useEffect(() => {
        if (pantryIngredientInit) {
            setIngredient({...pantryIngredientInit});
        }
        if (pantryIngredientInit?.expiration) {
            setExpiration(pantryIngredientInit.expiration);
        }
    }, [pantryIngredientInit]);
  
    return (
        <Modal show={show} onHide={handleClose} size="lg">
            <Modal.Header closeButton>
                <Modal.Title>{title}</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Form>
                    <IngredientInputFields
                        mode={mode}
                        ingredient={ingredient? ingredient as Ingredient : null}
                        handleChange={(ing) => setIngredient(ing)}
                    />
                    <InputGroup className={`my-3 ${styles.expiration_field}`}>
                        <InputGroup.Text id="expiration-date">
                            expiration date
                        </InputGroup.Text>
                        <Form.Control
                            defaultValue={expiration ? expiration : ""}
                            onChange={(e) => setExpiration(e.target.value)}
                            type="date"
                        />
                    </InputGroup>
                </Form>
            </Modal.Body>
            <Modal.Footer>
                <Button
                    className="custom_button"
                    onClick={ingredient? () => handleClick({
                            ...ingredient,
                            expiration: expiration
                        }) : () => {}}>
                    {buttonText}
                </Button>
            </Modal.Footer>
        </Modal>
    );
}
