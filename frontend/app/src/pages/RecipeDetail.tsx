import { useState } from 'react';
import { Button, Card, Col, Image, Row, Stack } from 'react-bootstrap';
import { useParams } from 'react-router-dom';
import recipes from '../data/recipe_detail.json';
import '../styles/RecipeDetail.css';
import plusCircleIcon from '../assets/plus_circle_icon.svg';
import minusCircleIcon from '../assets/minus_circle_icon.svg';
import { RecipeInfoCard } from '../components/RecipeInfoCard';

type Params = {
    id: string;
};


export function RecipeDetail() {
    const { id } = useParams<Params>();
    if (!id || !recipes.hasOwnProperty(id)) {
        return <div>Recipe not found</div>
    };
    const recipe = recipes[id];

    const [serving, setServing] = useState<number>(1);
    const updateServing = (amount: number): void => {
        const updatedAmount: number = Math.max(1, serving + amount);
        setServing(updatedAmount);
    };

    return (
        <>
            <Row md={2} xs={1} className="d-flex align-items-center g-2 mt-2">
                <Col className="image-container">
                    <Image
                        src={recipe.image}
                        alt={recipe.title}
                        className="image"
                        rounded
                    />
                </Col>
                <Col>
                    <RecipeInfoCard {...recipe}/>
                </Col>
            </Row>
            <Row md={2} xs={1} className="align-top g-2 mt-2">
                <Col md={4}>
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
                                {recipe.ingredients.map((
                                    ingredient: { name: string; quantity: number; unit: string;}
                                    ) => (
                                    <div className="text-wrap fs-5">
                                        {ingredient.name}:  {ingredient.quantity * serving} {ingredient.unit}
                                    </div>
                                ))}
                            </Stack>
                        </Card.Body>
                    </Card>
                    <Card className="p-3 mt-2">
                        <Card.Title>Notes</Card.Title>
                        <Card.Body>{recipe.notes}</Card.Body>
                    </Card>
                </Col>
                <Col md={8}>
                    <Card className="p-3 mt-2">
                        <Card.Title>Directions</Card.Title>
                        <Card.Body>
                            <Stack direction="vertical" gap={1} className="mt-2">
                                {recipe.directions.map((direction: string, index: number) => (
                                    <div key={index} className="mb-3">
                                        <h6>Step {index + 1}</h6>
                                        {direction}
                                    </div>
                                ))}
                            </Stack>
                        </Card.Body>
                    </Card>
                </Col>
            </Row>
        </>
    )   
}
