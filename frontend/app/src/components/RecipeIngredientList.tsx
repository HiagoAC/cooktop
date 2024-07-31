import { v4 as uuidv4 } from 'uuid';
import { useState } from 'react';
import { Button, Card, Stack } from 'react-bootstrap';
import { Ingredient } from '../types/interfaces';
import plusCircleIcon from '../assets/plus_circle_icon.svg';
import minusCircleIcon from '../assets/minus_circle_icon.svg';
import styles from '../styles/RecipeIngredientList.module.css'


interface Props {
    ingredients: Ingredient[],
}


export function RecipeIngredientList({ingredients}: Props) {
    const [serving, setServing] = useState<number>(1);
    const updateServing = (amount: number): void => {
        const updatedAmount: number = Math.max(1, serving + amount);
        setServing(updatedAmount);
    };

    return (
        <Card className="p-3 mt-2">
            <Card.Title>Ingredients</Card.Title>
            <Card.Subtitle className="mb-2 text-muted d-flex align-items-center">
                <span>servings</span>
                <Button
                    className={`${styles.plus_minus_button}`}
                    onClick={() => updateServing(1)}
                >
                    <img
                        src={plusCircleIcon}
                        alt="increase serving"
                        className={`${styles.plus_minus_icon}`}
                    />
                </Button>
                <span>{serving}</span>
                <Button
                    className={`${styles.plus_minus_button}`}
                    onClick={() => updateServing(-1)}
                >
                    <img
                        src={minusCircleIcon}
                        alt="decrease serving"
                        className={`${styles.plus_minus_icon}`}
                    />
                </Button>
            </Card.Subtitle>
            <Card.Body>
                <Stack direction="vertical" gap={1} >
                    {ingredients.map((
                        ingredient: Ingredient
                        ) => (
                        <div className="text-wrap fs-5" key={uuidv4()}>
                            {ingredient.name}:  {Number(ingredient.quantity) * serving} {ingredient.unit}
                        </div>
                    ))}
                </Stack>
            </Card.Body>
        </Card>
    )
}
