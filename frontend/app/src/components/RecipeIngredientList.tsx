import { v4 as uuidv4 } from 'uuid';
import { useState } from 'react';
import { Button, Card, Stack } from 'react-bootstrap';
import plusCircleIcon from '../assets/plus_circle_icon.svg';
import minusCircleIcon from '../assets/minus_circle_icon.svg';
import '../styles/RecipeIngredientList.css'


interface IngredientInfo {
    name: string,
    quantity: number,
    unit: string
}


interface Props {
    ingredients: IngredientInfo[],
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
                    className="plus-minus-button"
                    onClick={() => updateServing(1)}
                >
                    <img
                        src={plusCircleIcon}
                        alt="increase serving"
                        className="plus-minus-icon"
                    />
                </Button>
                <span>{serving}</span>
                <Button
                    className="plus-minus-button"
                    onClick={() => updateServing(-1)}
                >
                    <img
                        src={minusCircleIcon}
                        alt="decrease serving"
                        className="plus-minus-icon"
                    />
                </Button>
            </Card.Subtitle>
            <Card.Body>
                <Stack direction="vertical" gap={1} >
                    {ingredients.map((
                        ingredient: IngredientInfo
                        ) => (
                        <div className="text-wrap fs-5" key={uuidv4()}>
                            {ingredient.name}:  {ingredient.quantity * serving} {ingredient.unit}
                        </div>
                    ))}
                </Stack>
            </Card.Body>
        </Card>
    )
}
