import { useState } from 'react';
import { Button, Col, Form, Row } from 'react-bootstrap';

interface Props {
    withAddButton?: boolean;
    handleAdd?: (name: string, quantity: number, unit: string) => void;
}


export function IngredientInputFields({withAddButton=false, handleAdd}: Props) {
    const [formName, setFormName] = useState<string>('');
    const [formQuantity, setFormQuantity] = useState<number>(1);
    const [formUnit, setFormUnit] = useState<string>('unit');

    const handleUnitChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
        setFormUnit(event.target.value);
    };

    const measurementUnits = ['unit', 'teaspoon', 'tablespoon', 'cup', 'gram', 'ml'];

    return (
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
            {(withAddButton && handleAdd) ? (
                <Col>
                    <Button
                        variant="outline-secondary"
                        onClick={() => handleAdd(formName, formQuantity, formUnit)} 
                    >
                    + 
                    </Button>
                </Col>
            ) : null
            }
        </Row>
    );
}
