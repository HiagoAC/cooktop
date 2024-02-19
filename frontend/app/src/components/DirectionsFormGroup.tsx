import { v4 as uuidv4 } from 'uuid';
import { ReactElement, useState } from 'react';
import { Button, Card, Form, InputGroup, ListGroup } from 'react-bootstrap';
import '../styles/DirectionsFormGroup.css';


export function DirectionsFormGroup() {
    const [formStep, setFormStep] = useState<string>('');
    const [directions, setDirections] = useState<ReactElement[]>([]);

    const addStep = (): void => {
        const step =  <ListGroup.Item key={uuidv4()}>
            <div>Step {directions.length + 1}</div>
            <div>{formStep}</div>
        </ListGroup.Item>
        setDirections(prevDirections => [...prevDirections, step]);
        setFormStep('');
    };

    return (
        <Form.Group className="mb-3" controlId="directions">
            <Form.Label>Directions</Form.Label>
            <Card className="directions-card mb-2">
            <ListGroup variant="flush">
                {directions}
            </ListGroup>
            </Card>
            <InputGroup>
                <Form.Control
                    as="textarea"
                    placeholder="Type a step and press add."
                    value={formStep}
                    onChange={(e) => setFormStep(e.target.value)}
                />
                <Button variant="outline-secondary" onClick={() => addStep()}>
                    + 
                </Button>
            </InputGroup>
        </Form.Group>
    )
}
