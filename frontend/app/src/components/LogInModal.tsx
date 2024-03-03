import { useState } from 'react';
import { Button, Form, Modal } from 'react-bootstrap';
import { useAuth } from '../hooks/useAuth';


interface Props {
    show: boolean;
    handleClose: () => void;
}


export function LogInModal({show, handleClose}: Props) {
    const [email, setEmail] = useState<string>('');
    const [password, setPassword] = useState<string>('');
    const { logIn } = useAuth();

    const handleLogIn = async () => {
        logIn(email, password);
        handleClose();
    };

    return (
        <Modal show={show} onHide={handleClose}>
            <Modal.Header closeButton>
                <Modal.Title>{'Log In'}</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Form>
                    <Form.Group className="mb-3" controlId="emailAddress">
                        <Form.Label>{'Email'}</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="Email"
                            value={email}
                            onChange={
                                (e) => setEmail(e.target.value)}
                        />
                    </Form.Group>
                    <Form.Group className="mb-3" controlId="password">
                        <Form.Label>{'Password'}</Form.Label>
                        <Form.Control
                            type="password"
                            placeholder="Password"
                            value={password}
                            onChange={
                                (e) => setPassword(e.target.value)}
                        />
                    </Form.Group>
                </Form>
            </Modal.Body>
            <Modal.Footer>
                <Button
                    className="custom_button"
                    onClick={handleLogIn}
                >
                    {'Log In'}
                </Button>
            </Modal.Footer>
        </Modal>
    );
}
