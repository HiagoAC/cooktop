import { useEffect, useState } from 'react';
import {
    Button,
    ListGroup,
    Offcanvas as BaseOffcanvas,
} from 'react-bootstrap';
import { useAuth } from '../hooks/useAuth';
import styles from '../styles/Offcanvas.module.css';
import hamburgerIcon from '../assets/hamburger_icon.svg';
import signOutIcon from '../assets/sign_out_icon.svg';
import { getUser } from '../api/usersApi';
import { User } from '../types/interfaces';


export function Offcanvas() {
    const [show, setShow] = useState<boolean>(false);
    const [user, setUser] = useState<User | null>(null);
    const { logOut } = useAuth();

    const handleSignOut = () => {
        logOut();
        window.location.href = '/';
    }

    useEffect(() => {
        getUser().then((res) => {
            setUser(res.data);
        });

    }, []);

    return (
        <>
            <Button className={`${styles.button_hamburger}`} onClick={() => setShow(true)}>
                <img src={hamburgerIcon} alt="dropdown" className={`${styles.icon}`} />
            </Button>
            <BaseOffcanvas show={show} onHide={() => setShow(false)} placement="end">
            <BaseOffcanvas.Header closeButton>
                <BaseOffcanvas.Title></BaseOffcanvas.Title>
            </BaseOffcanvas.Header>
            <BaseOffcanvas.Body className={'d-flex flex-column justify-content-between'}>
                <ListGroup variant="flush" className={`${styles.offcanvas_list}`}>
                    <ListGroup.Item action href="/">Meal Plan</ListGroup.Item>
                    <ListGroup.Item action href="/recipes">Recipes</ListGroup.Item>
                    <ListGroup.Item action href="/shopping-list">Shopping List</ListGroup.Item>
                    <ListGroup.Item action href="/pantry">Pantry</ListGroup.Item>
                    <ListGroup.Item action href="about">About Cooktop</ListGroup.Item>
                    <ListGroup.Item action href="/account">Account Settings</ListGroup.Item>
                </ListGroup>
                <ListGroup variant="flush" className={`${styles.offcanvas_list} d-flex align-items-bottom`}>
                    <ListGroup.Item>
                        {`Signed in as ${user?.first_name} ${user?.last_name}`}
                    </ListGroup.Item>
                    <ListGroup.Item action onClick={handleSignOut}>
                        <div className={`${styles.icon_container}`}>
                            <img
                                src={signOutIcon}
                                alt="sign out"
                                className={`${styles.sign_out_icon}`}
                            />
                        </div> {'Sign Out'}
                    </ListGroup.Item>
                </ListGroup>
            </BaseOffcanvas.Body>
            </BaseOffcanvas>
        </>
    )
}
