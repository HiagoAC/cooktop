import { v4 as uuidv4 } from 'uuid';
import { ReactElement, useEffect, useState } from 'react';
import { Card, Form, ListGroup } from 'react-bootstrap';
import { IngredientInputFields } from './IngredientInputFields';
import { Ingredient } from '../types/interfaces';
import styles from '../styles/IngredientsFormGroup.module.css';


interface Props {
    ingredients: Ingredient[];
    setIngredients: (ingredients: Ingredient[]) => void;
}

export function IngredientsFormGroup({ingredients, setIngredients}: Props) {
    const [ingredientListItems, setIngredientListItems] = useState<ReactElement[]>([]);

    const addIngredient = (ingredient: Ingredient): void => {
        setIngredientListItems(prevDirections => [
            ...prevDirections,
            <ListGroup.Item key={uuidv4()}>
                <div>{ingredient.name} - {ingredient.quantity} {ingredient.display_unit}</div>
            </ListGroup.Item>
        ]);
        setIngredients([...ingredients, ingredient]);
    };

    useEffect(() => {
        if (ingredients) {
            ingredients.forEach((ingredient) => {
                addIngredient(ingredient);
            });
        }
    }, []);

    return (
        <Form.Group className="mb-3" controlId="ingredients">
            <Form.Label>Ingredients</Form.Label>
            <Card className={`mb-2 ${styles.ingredients_card}`}>
                <ListGroup variant="flush">
                    {ingredientListItems}
                </ListGroup>
            </Card>
            <IngredientInputFields withAddButton={true} handleAdd={addIngredient}/>
        </Form.Group>
    )
}
