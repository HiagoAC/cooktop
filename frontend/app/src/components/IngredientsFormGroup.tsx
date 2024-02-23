import { v4 as uuidv4 } from 'uuid';
import { ReactElement, useEffect, useState } from 'react';
import { Card, Form, ListGroup } from 'react-bootstrap';
import { IngredientInputFields } from './IngredientInputFields';
import { Ingredient } from '../data/recipe_detail';
import styles from '../styles/IngredientsFormGroup.module.css';


interface Props {
    initIngredients?: Ingredient[]
}

export function IngredientsFormGroup({initIngredients}: Props) {
    const [ingredients, setIngredients] = useState<ReactElement[]>([]);

    const addIngredient = (name: string, quantity: number, unit: string): void => {
        setIngredients(prevDirections => [
            ...prevDirections,
            <ListGroup.Item key={uuidv4()}>
                <div>{name} - {quantity} {unit}</div>
            </ListGroup.Item>
        ]);
    };

    useEffect(() => {
        if (initIngredients) {
            initIngredients.forEach((ingredient) => {
                addIngredient(ingredient.name, Number(ingredient.quantity), ingredient.unit);
            });
        }
    }, []);

    return (
        <Form.Group className="mb-3" controlId="ingredients">
            <Form.Label>Ingredients</Form.Label>
            <Card className={`mb-2 ${styles.ingredients_card}`}>
                <ListGroup variant="flush">
                    {ingredients}
                </ListGroup>
            </Card>
            <IngredientInputFields withAddButton={true} handleAdd={addIngredient}/>
        </Form.Group>
    )
}
