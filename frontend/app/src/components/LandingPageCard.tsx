import {  Card } from 'react-bootstrap';
import styles from '../styles/LandingPageCard.module.css';


interface Props {
    title: string,
    text: string
}

export function LandingPageCard({title, text}: Props) {
    return (
        <Card body className={`${styles.card} my-4`}>
            <Card.Title>{title}</Card.Title>
            <Card.Text>{text}</Card.Text>
        </Card>
    )
}
