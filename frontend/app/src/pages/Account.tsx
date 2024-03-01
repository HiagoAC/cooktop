import { Container } from 'react-bootstrap';
import { FormCard } from '../components/FormCard';
import { AccountForm } from '../components/AccountForm';
import { user, userPreferences } from '../data/user';


export function Account() {
    return (
        <Container className="pb-4">
            <FormCard
                title={`Account Settings - ${user.email}`}
                formComponent={<AccountForm initUser={user} initUserPreferences={userPreferences}/>}
                buttonText="Save"
            />
        </Container>
    )
}
