import { v4 as uuidv4 } from 'uuid';
import { useState } from 'react';
import { Button, Card, Form, InputGroup, ListGroup } from 'react-bootstrap';
import styles from '../styles/DirectionsFormGroup.module.css';


interface Props {
    directions: string[];
    setDirections: (directions: string[]) => void;
}

export function DirectionsFormGroup({directions, setDirections}: Props) {
    const [formDirection, setFormDirection] = useState<string>('');
    const [localDirections, setLocalDirections] = useState<string[]>(directions);

    const addDirection = (direction: string): void => {
        setFormDirection('');
        setLocalDirections([...localDirections, direction]);
        setDirections(localDirections);
    };

    return (
        <Form.Group className="mb-3" controlId="directions">
            <Form.Label>Directions</Form.Label>
            <Card className={`mb-2 ${styles.directions_card}`}>
            <ListGroup variant="flush">
                {directions.map((direction, index) => (
                    <ListGroup.Item key={uuidv4()}>
                        <div>Step {index + 1}</div>
                        <div>{direction}</div>
                    </ListGroup.Item>
                ))}
            </ListGroup>
            </Card>
            <InputGroup>
                <Form.Control
                    as="textarea"
                    placeholder="Type a step and press add."
                    value={formDirection}
                    onChange={(e) => setFormDirection(e.target.value)}
                />
                <Button
                    variant="outline-secondary"
                    onClick={() => addDirection(formDirection)}
                >
                    + 
                </Button>
            </InputGroup>
        </Form.Group>
    )
}
