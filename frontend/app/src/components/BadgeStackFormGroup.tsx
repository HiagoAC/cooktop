import { v4 as uuidv4 } from 'uuid';
import { Button, Form, InputGroup, Stack } from 'react-bootstrap';
import { ReactElement, useEffect, useState } from 'react';
import { Badge } from './Badge';
import '../styles/BadgeStackFormGroup.css';


interface Props {
    items?: string[],
    label: string,
    placeholder: string
}


export function BadgeStackFormGroup({items, label, placeholder}: Props) {
    const [formItem, setFormItem] = useState<string>('');
    const [addedItems, setAddedItems] = useState<ReactElement[]>([]);

    const addBadge = (item: string): void => {
        const badge = <Badge
            item={item}
            withDeleteButton={true}
            onDelete={deleteBadge}
            key={uuidv4()}
        />;
        setAddedItems(prevBadges => [...prevBadges, badge]);
        setFormItem('');
    };

    const deleteBadge = (item: string): void => {
        setAddedItems(prevBadges => {
            return prevBadges.filter(badge => badge.props.item !== item);
        });
    };

    useEffect(() => {
        if (items) {
            items.forEach(item => {
                addBadge(item);
            })}
    }, []);

    return (
        <Form.Group className="mb-3" controlId="tags">
            <Form.Label>{label}</Form.Label>
            <InputGroup>
                <Form.Control
                        type="text"
                        placeholder={placeholder}
                        value={formItem}
                        onChange={(e) => setFormItem(e.target.value)}
                />
                <Button variant="outline-secondary" onClick={() => addBadge(formItem)}>
                    + 
                </Button>
            </InputGroup>
            <Stack direction="horizontal" gap={1} className="mt-2 custom-stack">
                {addedItems}
            </Stack>
        </Form.Group>
    )
}
