import { useEffect, useState } from 'react';
import { Container } from 'react-bootstrap';
import { useAuth } from '../hooks/useAuth';
import { getUser } from '../api/usersApi';
import { FormCard } from '../components/FormCard';
import { AccountForm } from '../components/AccountForm';
import { User, userPreferences } from '../data/user';


export function Account() {
    const [user, setUser] = useState<User>();
    const { accessToken } = useAuth();
    useEffect(() => {
        getUser().then(res => {
            setUser({
                'email': res.data.email,
                'first_name': res.data.first_name,
                'last_name': res.data.last_name
            });
        });
    }, [accessToken]);
    return (
        <Container className="pb-4">
            { user? (
                <FormCard
                    title={`Account Settings - ${user.email}`}
                    formComponent={<AccountForm initUser={user} initUserPreferences={userPreferences}/>}
                    buttonText="Save"
                /> ) : (<></>)
            }
        </Container>
    )
}
