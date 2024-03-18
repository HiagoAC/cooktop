import { useEffect, useState } from 'react';
import { Ingredient } from '../types/interfaces';
import { Button, Col, Form, Row } from 'react-bootstrap';

interface Props {
    ingredient?: Ingredient | null;
    withAddButton?: boolean;
    handleAdd?: (ingredient: Ingredient) => void;
}


export function IngredientInputFields(
    {ingredient, withAddButton=false, handleAdd}
    : Props) {
    const [formName, setFormName] = useState<string>('');
    const [formQuantity, setFormQuantity] = useState<number>(1);
    const [formUnit, setFormUnit] = useState<string>('unit');

    useEffect(() => {
        if (ingredient) {
            setFormName(ingredient.name);
            setFormQuantity(Number(ingredient.quantity));
            setFormUnit(ingredient.unit);
        }
    }, [ingredient]);

    const handleUnitChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
        setFormUnit(event.target.value);
    };

    const measurementUnits = ['unit', 'teaspoon', 'tablespoon', 'cup', 'g', 'ml'];

    return (
        <Row md={4} xs={1} className="g-1">
            <Col md={6}>
                <Form.Control
                    type="text"
                    placeholder="Ingredient name"
                    value={formName}
                    onChange={(e) => setFormName(e.target.value)}
                />
            </Col>
            <Col md={2}>
                <Form.Control
                    type="number"
                    placeholder="Ingredient quantity."
                    value={formQuantity}
                    onChange={(e) => setFormQuantity(Number(e.target.value))}
                />
            </Col>
            <Col md={3}>
                <Form.Select
                    aria-label="Measurement Unit"
                    value={formUnit}
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
            {(withAddButton && handleAdd) ? (
                <Col md={1}>
                    <Button
                        variant="outline-secondary"
                        onClick={() => handleAdd({
                            name: formName,
                            quantity: formQuantity,
                            unit: formUnit
                        })}
                    >
                    + 
                    </Button>
                </Col>
            ) : null
            }
        </Row>
    );
}
