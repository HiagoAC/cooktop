import { Button, Card } from 'react-bootstrap';
import '../styles/FormCard.css';
import React from 'react';


interface Props {
    title: string,
    formComponent: React.ReactNode,
    buttonText: string
}


export function FormCard({title, formComponent, buttonText}: Props) {
    return (
        <div className="card-container">
            <Card className="my-2 custom-card">
                <Card.Header className="d-flex justify-content-center">
                    <Card.Title>{title}</Card.Title>
                </Card.Header>
                <Card.Body>
                    {formComponent}
                </Card.Body>
                <Card.Footer className="d-flex justify-content-center">
                    <Button className="mx-4 custom-button">
                        {buttonText}
                    </Button>
                </Card.Footer>
            </Card>
        </div>
    )
}
