import { useEffect, useState } from 'react';
import { Alert, Container } from 'react-bootstrap';
import { useAuth } from '../hooks/useAuth';
import { getUser, updateUser } from '../api/usersApi';
import { FormCard } from '../components/FormCard';
import { AccountForm } from '../components/AccountForm';
import { User } from '../types/interfaces';
import { getPreferences, updatePreferences } from '../api/preferencesApi';


export function Account() {
    const [user, setUser] = useState<User>();
    const { accessToken } = useAuth();
    const [cookings, setCookings] = useState<number>(4);
    const [servings, setServings] = useState<number>(2);
    const [
        preferencesUpdateSuccess,
        setPreferencesUpdateSuccess
    ] = useState<boolean | null>(null);
    const [
        userUpdateSuccess,
        setUserUpdateSuccess
    ] = useState<boolean | null>(null);

    useEffect(() => {
        getUser().then(res => {
            setUser({
                'email': res.data.email,
                'first_name': res.data.first_name,
                'last_name': res.data.last_name
            });
        });
    }, [accessToken]);

    useEffect(() => {
        getPreferences().then(res => {
            setCookings(res.data.cookings_per_week);
            setServings(res.data.servings_per_meal);
        });
    }, []);

    const handleSave = () => {
        if (!user) {
            return;
        }
        updateUser({
            first_name: user.first_name,
            last_name: user.last_name
        }).then(res => {
            if (res.status === 200) {
                setUserUpdateSuccess(true);
            } else {
                setUserUpdateSuccess(false);
            }
        });
        updatePreferences({
            cookings_per_week: cookings,
            servings_per_meal: servings
        }).then(res => {
            if (res.status === 200) {
                setPreferencesUpdateSuccess(true);
            } else {
                setPreferencesUpdateSuccess(false);
            }
        });
    };

    return (
        <Container className="pb-4">
            { preferencesUpdateSuccess && userUpdateSuccess? (
                <Alert variant="success" className="m-4">
                    {'Saved!'}
                </Alert>
            ) : preferencesUpdateSuccess === false ||
                userUpdateSuccess === false? (
                <Alert variant="danger" className="mb-4">
                    {'Request failed.'}
                </Alert>
            ) : (<></>)}
            { user? (
                <FormCard
                    title={`Account Settings - ${user.email}`}
                    formComponent={<AccountForm
                        user={user}
                        setUser={setUser}
                        cookings={cookings}
                        setCookings={setCookings}
                        servings={servings}
                        setServings={setServings}
                    />}
                    buttonText="Save"
                    handleClick={handleSave}
                /> ) : (<></>)
            }
        </Container>
    )
}
