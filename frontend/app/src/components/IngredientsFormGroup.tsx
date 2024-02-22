import { v4 as uuidv4 } from 'uuid';
import { ReactElement, useEffect, useState } from 'react';
import { Button, Card, Col, Form, ListGroup, Row } from 'react-bootstrap';
import { Ingredient } from '../data/recipe_detail';
import '../styles/DirectionsFormGroup.css';


interface Props {
    initIngredients?: Ingredient[]
}

export function IngredientsFormGroup({initIngredients}: Props) {
    const [formName, setFormName] = useState<string>('');
    const [formQuantity, setFormQuantity] = useState<number>(1);
    const [formUnit, setFormUnit] = useState<string>('unit');
    const [ingredients, setIngredients] = useState<ReactElement[]>([]);

    const addIngredient = (name: string, quantity: number, unit: string): void => {
        setIngredients(prevDirections => [
            ...prevDirections,
            <ListGroup.Item key={uuidv4()}>
                <div>{name} - {quantity} {unit}</div>
            </ListGroup.Item>
        ]);
    };

    const handleUnitChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
        setFormUnit(event.target.value);
    };

    useEffect(() => {
        if (initIngredients) {
            initIngredients.forEach((ingredient) => {
                addIngredient(ingredient.name, Number(ingredient.quantity), ingredient.unit);
            });
        }
    }, []);

    const measurementUnits = ['unit', 'teaspoon', 'tablespoon', 'cup', 'gram', 'ml'];

    return (
        <Form.Group className="mb-3" controlId="directions">
            <Form.Label>Ingredients</Form.Label>
            <Card className="directions-card mb-2">
            <ListGroup variant="flush">
                {ingredients}
            </ListGroup>
            </Card>
            <Row lg={4} md={2} xs={1} className="g-1">
                <Col>
                    <Form.Control
                        type="text"
                        placeholder="Ingredient name"
                        value={formName}
                        onChange={(e) => setFormName(e.target.value)}
                    />
                </Col>
                <Col>
                    <Form.Control
                        type="number"
                        placeholder="Ingredient quantity."
                        value={formQuantity}
                        onChange={(e) => setFormQuantity(Number(e.target.value))}
                    />
                </Col>
                <Col>
                    <Form.Select
                        aria-label="Measurement Unit"
                        defaultValue={"default"}
                        onChange={handleUnitChange}
                    >
                        <option key="default" disabled>Measurement Unit</option>
                        {measurementUnits.map((measurementUnit) => (
                            <option
                                key={measurementUnit}
                                value={measurementUnit}
                            >
                                {measurementUnit}
                            </option>
                        ))}
                    </Form.Select>
                </Col>
                <Col>
                    <Button
                        variant="outline-secondary"
                        onClick={() => addIngredient(formName, formQuantity, formUnit)} 
                    >
                    + 
                    </Button>
                </Col>
            </Row>
        </Form.Group>
    )
}
