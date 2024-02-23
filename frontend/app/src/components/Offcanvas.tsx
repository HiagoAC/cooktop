import { useState } from 'react';
import {
    Button,
    ListGroup,
    Offcanvas as BaseOffcanvas,
} from 'react-bootstrap';
import styles from '../styles/Offcanvas.module.css';
import hamburgerIcon from '../assets/hamburger_icon.svg';


export function Offcanvas() {
    const [show, setShow] = useState(false);

    return (
        <>
            <Button className={`${styles.button_hamburger}`} onClick={() => setShow(true)}>
                <img src={hamburgerIcon} alt="dropdown" className={`${styles.icon}`} />
            </Button>
            <BaseOffcanvas show={show} onHide={() => setShow(false)} placement="end">
            <BaseOffcanvas.Header closeButton>
                <BaseOffcanvas.Title></BaseOffcanvas.Title>
            </BaseOffcanvas.Header>
            <BaseOffcanvas.Body>
                <ListGroup variant="flush" className={`${styles.offcanvas_list}`}>
                    <ListGroup.Item action href="/">Meal Plan</ListGroup.Item>
                    <ListGroup.Item action href="/recipes">Recipes</ListGroup.Item>
                    <ListGroup.Item action href="/shopping-list">Shopping List</ListGroup.Item>
                    <ListGroup.Item action href="/pantry">Pantry</ListGroup.Item>
                    <ListGroup.Item action href="#">About Cooktop</ListGroup.Item>
                    <ListGroup.Item action href="/me">Account & Settings</ListGroup.Item>
                </ListGroup>
            </BaseOffcanvas.Body>
            </BaseOffcanvas>
        </>
    )
}