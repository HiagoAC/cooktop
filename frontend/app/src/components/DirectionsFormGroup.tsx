import { v4 as uuidv4 } from 'uuid';
import { ReactElement, useEffect, useState } from 'react';
import { Button, Card, Form, InputGroup, ListGroup } from 'react-bootstrap';
import styles from '../styles/DirectionsFormGroup.module.css';


interface Props {
    directions: string[];
    setDirections: (directions: string[]) => void;
}

export function DirectionsFormGroup({directions, setDirections}: Props) {
    const [formDirection, setFormDirection] = useState<string>('');
    const [directionItems, setDirectionItems] = useState<ReactElement[]>([]);

    const addDirection = (direction: string): void => {
        setDirectionItems(prevDirections => [
            ...prevDirections,
            <ListGroup.Item key={uuidv4()}>
                <div>Step {prevDirections.length + 1}</div>
                <div>{direction}</div>
            </ListGroup.Item>
        ]);
        setFormDirection('');
        setDirections([...directions, direction]);
    };
    useEffect(() => {
        if (directions) {
            directions.forEach((direction) => {
                addDirection(direction);
            });
        }
    });

    return (
        <Form.Group className="mb-3" controlId="directions">
            <Form.Label>Directions</Form.Label>
            <Card className={`mb-2 ${styles.directions_card}`}>
            <ListGroup variant="flush">
                {directionItems}
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
