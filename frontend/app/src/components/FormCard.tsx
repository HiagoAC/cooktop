import { Button, Card } from 'react-bootstrap';
import styles from '../styles/FormCard.module.css';
import React from 'react';


interface Props {
    title: string;
    formComponent: React.ReactNode;
    buttonText: string;
    handleClick: () => void;
}


export function FormCard({title, formComponent, buttonText, handleClick}: Props) {
    return (
        <div className={`${styles.card_container}`}>
            <Card className={`my-2 ${styles.custom_card}`}>
                <Card.Header className="d-flex justify-content-center">
                    <Card.Title>{title}</Card.Title>
                </Card.Header>
                <Card.Body>
                    {formComponent}
                </Card.Body>
                <Card.Footer className="d-flex justify-content-center">
                    <Button
                        className={`mx-4 ${styles.custom_button}`}
                        onClick={handleClick}
                    >
                        {buttonText}
                    </Button>
                </Card.Footer>
            </Card>
        </div>
    )
}
