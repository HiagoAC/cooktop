import { useEffect, useState } from 'react';
import { Button, Col, Form, Row } from 'react-bootstrap';
import { ChangePasswordModal } from './ChangePasswordModal';
import { UserPreferencesFormFields } from './UserPreferencesFormFields';
import { User, UserPreferences } from '../data/user';
import { getPreferences } from '../api/preferencesApi';


interface Props {
    initUser: User;
}

export function AccountForm({initUser}: Props) {
    const [user, setUser] = useState<User>(initUser);
    const [passwordModalShow, setPasswordModalShow] = useState(false);
    const [cookings, setCookings] = useState<number>(4);
    const [servings, setServings] = useState<number>(2);

    useEffect(() => {
        getPreferences().then(res => {
            setCookings(res.data.cookings_per_week);
            setServings(res.data.servings_per_meal);
        });
    }, []);

    const handleFirstNameChange = (
        event: React.ChangeEvent<HTMLInputElement>) => {
        setUser({
            ...user,
            first_name: event.target.value
        });
    };

    const handleLastNameChange = (
        event: React.ChangeEvent<HTMLInputElement>) => {
        setUser({
            ...user,
            last_name: event.target.value
        });
    };

    const handlePasswordModalClose = () => setPasswordModalShow(false);
    const handlePasswordModalShow = () => setPasswordModalShow(true);

    return (
        <Form className="p-3">
            <Button
                className="mb-3 custom_button"
                onClick={handlePasswordModalShow}
            >
                {'Change Password'}
            </Button>
            <ChangePasswordModal
                show={passwordModalShow}
                handleClose={handlePasswordModalClose}
            />
            <Row>
                <Col>
                    <Form.Group className="mb-3" controlId="firstName">
                        <Form.Label>{'First Name'}</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="First Name"
                            value={user.first_name}
                            onChange={handleFirstNameChange}
                        />
                    </Form.Group> 
                </Col>
                <Col>
                    <Form.Group className="mb-3" controlId="lastName">
                        <Form.Label>{'Last Name'}</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="Last Name"
                            value={user.last_name}
                            onChange={handleLastNameChange}
                        />
                    </Form.Group>
                </Col>
                <UserPreferencesFormFields
                        cookings={cookings}
                        setCookings={setCookings}
                        servings={servings}
                        setServings={setServings}
                    />
            </Row>
        </Form>
    )
}
