import React from 'react';

interface Props<T> {
	children: JSX.Element | JSX.Element[];
	value?: T;
}

export interface GenericContext<T> {
	Context: React.Context<T | undefined>;
	ContextProvider: ({ children, value }: Props<T>) => JSX.Element;
	useContext: () => T;
}

export function createGenericContext<T>(initValue?: T): GenericContext<T> {
	const Context = React.createContext<T | undefined>(undefined);

	function ContextProvider({ children, value }: Props<T>): JSX.Element {
		if (!value && !initValue) {
			throw new Error('The generic context has not been provided with any value.');
		} else if (initValue && value) {
			throw new Error(
				'Cannot pass a value to a generic context provider when ' + 
				'the context has been created with an initial value.');
		}
		return (
			<Context.Provider value={initValue || value}>
				{children}
			</Context.Provider>
		);
	}

	function useContext(): T {
		const value = React.useContext(Context);
		if (value === undefined) {
			throw new Error(
				'A generic context can be only used from within the ' +
				'generic context provider that is associated with it.'
			)
		} else {
			return value;
		}
	}

	return { Context, ContextProvider, useContext };
}